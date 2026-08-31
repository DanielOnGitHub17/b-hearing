# cURL and HTTPie examples

This document covers common request patterns for testing the Django API, including authentication, JSON payloads, form uploads, and other HTTP methods.

## 1. Basic patterns

### GET request

```bash
curl -u username:password "http://localhost:8000/your-endpoint/"
```

```bash
http GET http://localhost:8000/your-endpoint/ --auth username:password
```

### GET request with explicit headers

```bash
curl -H "Accept: application/json" \
     -H "Content-Type: application/json" \
     -u username:password \
     "http://localhost:8000/your-endpoint/"
```

```bash
http GET http://localhost:8000/your-endpoint/ \
  Accept:application/json \
  Content-Type:application/json \
  --auth username:password
```

### Bearer token

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     "http://localhost:8000/your-endpoint/"
```

```bash
http GET http://localhost:8000/your-endpoint/ \
  Authorization:'Bearer YOUR_TOKEN' \
  Content-Type:application/json
```

---

## 2. JSON requests

### POST JSON

```bash
curl -X POST \
     -u username:password \
     -H "Content-Type: application/json" \
     -d '{"field":"value","name":"Alice"}' \
     "http://localhost:8000/your-endpoint/"
```

```bash
http POST http://localhost:8000/your-endpoint/ \
  field=value \
  name='Alice' \
  Content-Type:application/json \
  --auth username:password
```

### POST raw JSON via stdin

```bash
echo '{"field":"value","name":"Alice"}' | \
http POST http://localhost:8000/your-endpoint/ \
  Content-Type:application/json \
  --auth username:password
```

### PUT JSON

```bash
curl -X PUT \
     -u username:password \
     -H "Content-Type: application/json" \
     -d '{"field":"updated-value"}' \
     "http://localhost:8000/your-endpoint/1/"
```

```bash
http PUT http://localhost:8000/your-endpoint/1/ \
  field='updated-value' \
  Content-Type:application/json \
  --auth username:password
```

### PATCH JSON

```bash
curl -X PATCH \
     -u username:password \
     -H "Content-Type: application/json" \
     -d '{"field":"partial-update"}' \
     "http://localhost:8000/your-endpoint/1/"
```

```bash
http PATCH http://localhost:8000/your-endpoint/1/ \
  field='partial-update' \
  Content-Type:application/json \
  --auth username:password
```

---

## 3. Form data

### Form-encoded POST

```bash
curl -X POST \
     -u username:password \
     -H "Content-Type: application/x-www-form-urlencoded" \
     --data "username=alice&password=secret" \
     "http://localhost:8000/login/"
```

```bash
http --form POST http://localhost:8000/login/ \
  username=alice \
  password=secret \
  --auth username:password
```

### Multipart form upload

```bash
curl -X POST \
     -u username:password \
     -F "title=My File" \
     -F "file=@/path/to/file.txt" \
     "http://localhost:8000/upload/"
```

```bash
http --form POST http://localhost:8000/upload/ \
  title='My File' \
  file@/path/to/file.txt \
  --auth username:password
```

---

## 4. Delete and non-CRUD patterns

### DELETE request

```bash
curl -X DELETE \
     -u username:password \
     "http://localhost:8000/your-endpoint/1/"
```

```bash
http DELETE http://localhost:8000/your-endpoint/1/ --auth username:password
```

### HEAD request

```bash
curl -I "http://localhost:8000/your-endpoint/"
```

```bash
http HEAD http://localhost:8000/your-endpoint/
```

### OPTIONS request

```bash
curl -X OPTIONS "http://localhost:8000/your-endpoint/" -i
```

```bash
http OPTIONS http://localhost:8000/your-endpoint/
```

---

## 5. Common request-building patterns

### Without authentication

```bash
curl "http://localhost:8000/your-endpoint/"
```

```bash
http GET http://localhost:8000/your-endpoint/
```

### With basic auth in URL form

```bash
curl "http://username:password@localhost:8000/your-endpoint/"
```

### Send custom headers

```bash
curl -H "X-API-Key: abc123" \
     -H "Accept: application/json" \
     "http://localhost:8000/your-endpoint/"
```

```bash
http GET http://localhost:8000/your-endpoint/ \
  X-API-Key:abc123 \
  Accept:application/json
```

### Save response to a file

```bash
curl -u username:password "http://localhost:8000/your-endpoint/" -o response.json
```

```bash
http GET http://localhost:8000/your-endpoint/ --auth username:password > response.json
```

---

## 6. Quick mental model

- GET: read data
- POST: create data
- PUT: replace data
- PATCH: partially update data
- DELETE: remove data
- HEAD: metadata only
- OPTIONS: supported methods and capabilities

Use the correct Content-Type header based on the payload:

- JSON: application/json
- Form data: application/x-www-form-urlencoded
- File upload: multipart/form-data

Use the same pattern for any Django endpoint: set the URL, add auth as needed, and match the Content-Type to the payload you are sending.
