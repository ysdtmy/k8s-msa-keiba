# Prediction Worker

集約されたデータに基づいてレース予測を生成する専門的なワーカーサービスです。

## コンテナ情報

- **ベースイメージ**: `python:3.12-slim-bookworm`
- **ユーザー**: `appuser` (UID 1000)
- **ポート**: 8083

## ビルドと実行

### ビルド
```bash
docker build -t prediction .
```

### 実行
```bash
docker run -p 8083:8083 prediction
```

## 環境変数

| 変数名 | 説明 | デフォルト値 |
|----------|-------------|---------|
| `APP_PORT` | アプリケーションがリッスンするポート | `8083` |
| `OTEL_SERVICE_NAME` | OpenTelemetryサービス名 | `prediction` |
