# Odds Worker

オッズ情報の取得と分析を担当する専門的なワーカーサービスです。

## コンテナ情報

- **ベースイメージ**: `python:3.12-slim-bookworm`
- **ユーザー**: `appuser` (UID 1000)
- **ポート**: 8082

## ビルドと実行

### ビルド
```bash
docker build -t odds .
```

### 実行
```bash
docker run -p 8082:8082 odds
```

## 環境変数

| 変数名 | 説明 | デフォルト値 |
|----------|-------------|---------|
| `APP_PORT` | アプリケーションがリッスンするポート | `8082` |
| `OTEL_SERVICE_NAME` | OpenTelemetryサービス名 | `odds` |
