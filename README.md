# IP Nexsus

Cloudflare Workers uygulaması - IP geolocation ve analiz aracı.

## Geliştirme Ortamı Kurulumu

### 1. Bağımlılıkları Yükleyin

```bash
pnpm install
```

### 2. Environment Variables Yapılandırması

Local geliştirme için `.dev.vars` dosyası oluşturun:

```bash
cp .dev.vars.example .dev.vars
```

`.dev.vars` dosyasını düzenleyerek gerekli API anahtarlarını ekleyin:

```env
MAPBOX_ACCESS_TOKEN=your_actual_mapbox_token
```

### 3. Local Geliştirme Sunucusunu Başlatın

```bash
pnpm dev
# veya
wrangler dev
```

Uygulama `http://localhost:8787` adresinde çalışacaktır.

## Production Deployment

### Environment Variables Ayarlama

Production ortamı için environment variables'ı Cloudflare Dashboard üzerinden veya wrangler CLI ile ayarlayın:

#### Cloudflare Dashboard ile:
1. Workers & Pages > Your Worker > Settings > Variables
2. Environment Variables bölümünden ekleyin

#### Wrangler CLI ile:
```bash
wrangler secret put MAPBOX_ACCESS_TOKEN
```

### Deploy

```bash
pnpm deploy
# veya
wrangler deploy
```

## Proje Yapısı

```
.
├── src/
│   └── index.js          # Worker entry point
├── public/
│   └── index.html        # Frontend HTML
├── wrangler.jsonc        # Cloudflare Workers config
├── .dev.vars            # Local environment variables (gitignored)
└── .dev.vars.example    # Environment variables template
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MAPBOX_ACCESS_TOKEN` | Mapbox API access token | Yes |

## Notlar

- `.dev.vars` dosyası otomatik olarak gitignore edilmiştir
- Production environment variables Cloudflare Dashboard'dan yönetilmelidir
- Local geliştirmede `wrangler dev` komutu `.dev.vars` dosyasını otomatik olarak yükler

