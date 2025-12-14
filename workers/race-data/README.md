# Race Data Worker

レース情報を取得・処理する役割を持つ専門的なワーカーサービスです。

## コンテナ情報

- **ベースイメージ**: `python:3.12-slim-bookworm`
- **ユーザー**: `appuser` (UID 1000)
- **ポート**: 8081

## ビルドと実行

### ビルド
```bash
docker build -t race-data .
```

### 実行
```bash
docker run -p 8081:8081 race-data
```

## 環境変数

| 変数名 | 説明 | デフォルト値 |
|----------|-------------|---------|
| `APP_PORT` | アプリケーションがリッスンするポート | `8081` |
| `OTEL_SERVICE_NAME` | OpenTelemetryサービス名 | `race-data` |
