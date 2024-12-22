# url_shorten_service

## API Endpoints

### Create Short URL

```{bash}
POST /shorten
{
    "url": "https://www.google.com"
}
```

### Retrieve Original URL

```{bash}
GET /<short_url>
```

### Update short URL

```{bash}
PUT /<short_url>
{
    "url": "https://www.newgoogle.com"
}
```

### Delete short URL

```{bash}
DELETE /<short_url>
```

### Get URL Statistics

```{bash}
GET /<short_url>/stats
```

## How to run

### Run the server

```{bash}
python server.py
```

### Run the GUI client

```{bash}
python gui_client.py
```
