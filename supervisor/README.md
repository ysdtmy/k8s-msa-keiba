# Supervisor Service

K8sマルチエージェントシステムの中心的なコーディネーターサービスです。LangGraphワークフローを管理し、専門的なワーカー間の相互作用を調整します。

## コンテナ情報

- **ベースイメージ**: `python:3.12-slim-bookworm`
- **ユーザー**: `appuser` (UID 1000)
- **ポート**: 8080

## ビルドと実行

### ビルド
```bash
docker build -t supervisor .
```

### 実行
```bash
docker run -p 8080:8080 supervisor
```

## 環境変数

| 変数名 | 説明 | デフォルト値 |
|----------|-------------|---------|
| `APP_PORT` | アプリケーションがリッスンするポート | `8080` |
| `OTEL_SERVICE_NAME` | OpenTelemetryサービス名 | `supervisor` |
