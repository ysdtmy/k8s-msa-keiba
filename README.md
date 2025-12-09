# K8s Multi-Agent System (Horse Racing Prediction)

Kubernetes (Minikube), Dapr, LangGraph を利用したマルチエージェント競馬予想システムのサンプル実装です。
WSL (Ubuntu) 環境での実行を想定しています。

## 前提条件 (Prerequisites)

以下のツールが WSL (Ubuntu) 環境にインストールされていること。

- **WSL 2** (Ubuntu 22.04 推奨)
- **Docker Desktop**: Windows側にインストールし、WSL 2 Integration を有効に設定済みであること。
- **Minikube**: Dockerドライバーを使用。
- **kubectl**: クラスタ操作用。
- **Helm**: Dapr のインストールに使用。
- **uv**: Python パッケージ管理およびプロジェクト管理に使用。

## セットアップ & 起動 (Setup & Start)

### 1. Minikube の起動

```bash
minikube start
```

### 2. Dapr のインストール (初回のみ)

Helm を使用して Dapr を K8s クラスタにインストールします。

```bash
# Helm リポジトリの追加
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update

# Dapr のインストール
helm upgrade --install dapr dapr/dapr --version=1.14 --namespace dapr-system --create-namespace --wait
```

### 3. アプリケーションのビルド

各エージェント (Supervisor, Workers) の Docker イメージを Minikube の Docker 環境内にビルドします。

```bash
# Supervisor (LangGraph)
minikube image build -t supervisor:latest ./supervisor

# Worker Agents
minikube image build -t worker-race-data:latest ./workers/race-data
minikube image build -t worker-odds:latest ./workers/odds
minikube image build -t worker-prediction:latest ./workers/prediction
```

### 4. デプロイ

K8s マニフェストを適用して、Redis, Dapr Component, および各エージェントをデプロイします。

```bash
# Redis & Dapr Components
kubectl apply -f deploy/redis.yaml
kubectl apply -f deploy/components/statestore.yaml

# Agents
kubectl apply -f deploy/supervisor.yaml
kubectl apply -f deploy/worker-race-data.yaml
kubectl apply -f deploy/worker-odds.yaml
kubectl apply -f deploy/worker-prediction.yaml
```

### 5. 状態確認

全ての Pod が `Running` (Ready: 2/2) になるまで待ちます。

```bash
kubectl get pods -w
```

## 動作検証 (Verification)

Supervisor Agent に対して API リクエストを送信し、マルチエージェントによる予測を実行します。
`curl` コマンドがコンテナ内に含まれていないため、Python を使用してリクエストします。

```bash
kubectl exec deploy/supervisor -c supervisor -- /app/.venv/bin/python -c "import requests; print(requests.post('http://localhost:8080/predict', json={'race_id': '202305280511'}).json())"
```

**成功時の出力例:**
```json
{
  "prediction": {
    "winner": "Equinox",
    "confidence": "High",
    "reasoning": "Strong performance in fetch_data and odds analysis."
  },
  "messages": [
    ... (ツール呼び出しの履歴) ...
  ]
}
```

## 開発 (Development)

### 依存関係の追加
各ディレクトリ (`supervisor`, `workers/*`) で `uv` を使用します。

```bash
cd supervisor
uv add <package_name>
```

### 再デプロイ
コードを変更した場合、イメージの再ビルドと Pod の再起動が必要です。

```bash
# 1. 再ビルド (例: supervisor)
minikube image build -t supervisor:latest ./supervisor

# 2. Pod 再起動
kubectl rollout restart deployment/supervisor
```

## 構成概要

- **Supervisor**: LangGraph を使用した監督エージェント。ユーザーリクエストを解釈し、ToolNode を通じて Worker を呼び出します。
- **Workers**: 特定のタスクを実行する Dapr サービス。現在は Mock データを返します。
    - `worker-race-data`: レース情報取得
    - `worker-odds`: オッズ分析
    - `worker-prediction`: 最終予想
- **Dapr**: サイドカーによるサービス間通信 (Service Invocation) を担当。
- **Redis**: Dapr State Store (今回の実装ではアプリからの明示的な利用はなし)。
