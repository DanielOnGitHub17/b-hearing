# API spec for creating records

This document describes the create endpoints for the Django REST API used by the selections app. It is based on the actual models and serializers in the project.

Base URL:

```text
http://127.0.0.1:2851
```

Authentication:

- All create endpoints require authentication.
- The project uses DRF `permissions.IsAuthenticated` for the viewsets.
- Use HTTP Basic Auth in curl, or `--auth username:password` in HTTPie.
- The server sets `owner` automatically on `Selection` creation; clients should not send it.

Headers for all JSON requests:

```http
Content-Type: application/json
Accept: application/json
```

Typical auth examples:

```bash
curl -u username:password -H "Content-Type: application/json" http://127.0.0.1:2851/selections/
```

```bash
http --auth username:password POST http://127.0.0.1:2851/selections/ Content-Type:application/json
```

---

## Endpoint-to-model mappings

This API is a thin DRF layer over the following model/serializer pairs:

- `POST /selections/` maps to the `Selection` model through `SelectionSerializer`
- `GET /selections/{id}/` maps to the `Selection` model through `SelectionDetailSerializer`
- `POST /audiosources/` maps to `AudioSourceSuggestion` through `AudioSourceSerializer`
- `POST /audiooffsets/` maps to `AudioOffsetSuggestion` through `AudioOffsetSerializer`
- `POST /verseranges/` maps to `VerseRange` through `VerseRangeSerializer`

Important contract notes:

- `owner` is set by the server when creating a selection.
- `audio_source` is optional and may be `null`.
- `label` must be unique.
- `browser_voice` is the selection voice field.
- `start_verse` and `end_verse` must be valid verse IDs, and `start_verse <= end_verse`.
- `selection` must reference an existing selection owned by the authenticated user.
- `position` is assigned automatically when omitted.

---

## 1) Create a Selection

Endpoint:

```text
POST /selections/
```

Required fields:

- `label`: unique string
- `browser_voice`: string, default is `"default"`
- `repeat`: integer
- `version`: string, such as `"kjv"`
- `read_label`: boolean, default `false`
- `audio_source`: optional integer id or `null`

### Example payload

```json
{
  "audio_source": 1,
  "label": "Genesis 1-2",
  "browser_voice": "default",
  "repeat": 2,
  "version": "kjv",
  "read_label": false
}
```

### curl

```bash
curl -X POST \
  -u username:password \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "audio_source": 1,
    "label": "Genesis 1-2",
    "browser_voice": "default",
    "repeat": 2,
    "version": "kjv",
    "read_label": false
  }' \
  http://127.0.0.1:2851/selections/
```

### httpie

```bash
http --auth username:password POST http://127.0.0.1:2851/selections/ \
  audio_source:=1 \
  label='Genesis 1-2' \
  browser_voice='default' \
  repeat:=2 \
  version='kjv' \
  read_label:=false \
  Content-Type:application/json
```

### Response shape

```json
{
  "id": 1,
  "owner": "user@example.com",
  "label": "Genesis 1-2",
  "browser_voice": "default",
  "audio_source": 1,
  "repeat": 2,
  "version": "kjv",
  "read_label": false,
  "verse_ranges_length": 0
}
```

---

## 2) Create an Audio Source Suggestion

Endpoint:

```text
POST /audiosources/
```

This endpoint maps to `AudioSourceSuggestion`, which inherits from `AudioSource`.

Fields accepted by the serializer:

- `url_template`: required string
- `name`: required string
- `version`: optional string, default `"King James Version"`
- `version_abbr`: optional string, default `"KJV"`

### Example payload

```json
{
  "url_template": "https://example.com/audio/%(book_no)s/%(chapter_no)s.mp3",
  "name": "Example KJV Audio",
  "version": "King James Version",
  "version_abbr": "KJV"
}
```

### curl

```bash
curl -X POST \
  -u username:password \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "url_template": "https://example.com/audio/%(book_no)s/%(chapter_no)s.mp3",
    "name": "Example KJV Audio",
    "version": "King James Version",
    "version_abbr": "KJV"
  }' \
  http://127.0.0.1:2851/audiosources/
```

### httpie

```bash
http --auth username:password POST http://127.0.0.1:2851/audiosources/ \
  url_template='https://example.com/audio/%(book_no)s/%(chapter_no)s.mp3' \
  name='Example KJV Audio' \
  version='King James Version' \
  version_abbr='KJV' \
  Content-Type:application/json
```

### Response shape

```json
{
  "url_template": "https://example.com/audio/%(book_no)s/%(chapter_no)s.mp3",
  "name": "Example KJV Audio",
  "version": "King James Version",
  "version_abbr": "KJV"
}
```

---

## 3) Create an Audio Offset Suggestion

Endpoint:

```text
POST /audiooffsets/
```

This maps to `AudioOffsetSuggestion`, which inherits from `AudioOffset`.

Fields:

- `source`: required integer ID of an `AudioSource`
- `verse`: required integer ID of a `Verse`

### Example payload

```json
{
  "source": 1,
  "verse": 123
}
```

### curl

```bash
curl -X POST \
  -u username:password \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "source": 1,
    "verse": 123
  }' \
  http://127.0.0.1:2851/audiooffsets/
```

### httpie

```bash
http --auth username:password POST http://127.0.0.1:2851/audiooffsets/ \
  source:=1 \
  verse:=123 \
  Content-Type:application/json
```

### Response shape

```json
{
  "source": 1,
  "verse": 123
}
```

Notes:

- `source` must exist in the `audiosource` table.
- `verse` must exist in the `verse` table.
- A suggestion represents a proposed mapping between a verse and an audio source.

---

## 4) Create a Verse Range

Endpoint:

```text
POST /verseranges/
```

Fields:

- `selection`: required integer ID of the selection this range belongs to
- `start_verse`: required integer ID of the starting verse
- `end_verse`: required integer ID of the ending verse
- `position`: optional integer; if omitted, the model auto-calculates it in `VerseRange.save()`

### Example payload

```json
{
  "selection": 1,
  "start_verse": 10,
  "end_verse": 25
}
```

### curl

```bash
curl -X POST \
  -u username:password \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "selection": 1,
    "start_verse": 10,
    "end_verse": 25
  }' \
  http://127.0.0.1:2851/verseranges/
```

### httpie

```bash
http --auth username:password POST http://127.0.0.1:2851/verseranges/ \
  selection:=1 \
  start_verse:=10 \
  end_verse:=25 \
  Content-Type:application/json
```

### Response shape

```json
{
  "id": 1,
  "position": 1,
  "selection": 1,
  "start_verse": 10,
  "end_verse": 25,
  "verses": [
    {"book": 1, "chapter": 1, "verse": 10, "kjv": "..."},
    {"book": 1, "chapter": 1, "verse": 11, "kjv": "..."}
  ]
}
```

Notes:

- `position` is assigned automatically if not included.
- The serializer builds `verses` from the inclusive range between `start_verse` and `end_verse` using `Verse.objects.filter(id__range=(...))`.
- `selection` must correspond to a valid existing selection for the authenticated user or at least a valid selection row.

---

## Validation and edge cases

These are the most likely problems when testing the endpoints.

### Selection

- `label` must be unique.
- `audio_source` may be omitted or `null`.
- `repeat` must be an integer.
- `version` is required.

### Audio source suggestion

- `url_template` should include placeholders such as `%(book_no)s`, `%(chapter_no)s`, or `%(book_name_abbr)s`.
- `name` should be a human-readable identifier.
- `version_abbr` is usually a short code like `KJV` or `NIV`.

### Audio offset suggestion

- `source` must be a valid `AudioSource` id.
- `verse` must be a valid `Verse` id.

### Verse range

- `start_verse` and `end_verse` should be valid verse IDs.
- Ideally `end_verse >= start_verse`.
- `selection` must be a valid selection row.

---

## Quick command checklist

Create a selection:

```bash
curl -u username:password -H "Content-Type: application/json" -d '{"label":"Genesis 1-2","browser_voice":"default","repeat":2,"version":"kjv","read_label":false}' http://127.0.0.1:2851/selections/
```

Create an audio source suggestion:

```bash
curl -u username:password -H "Content-Type: application/json" -d '{"url_template":"https://example.com/audio/%(book_no)s/%(chapter_no)s.mp3","name":"Example KJV Audio","version":"King James Version","version_abbr":"KJV"}' http://127.0.0.1:2851/audiosources/
```

Create an audio offset suggestion:

```bash
curl -u username:password -H "Content-Type: application/json" -d '{"source":1,"verse":123}' http://127.0.0.1:2851/audiooffsets/
```

Create a verse range:

```bash
curl -u username:password -H "Content-Type: application/json" -d '{"selection":1,"start_verse":10,"end_verse":25}' http://127.0.0.1:2851/verseranges/
```

HTTPie equivalents:

```bash
http --auth username:password POST http://127.0.0.1:2851/selections/ label='Genesis 1-2' browser_voice='default' repeat:=2 version='kjv' read_label:=false
http --auth username:password POST http://127.0.0.1:2851/audiosources/ url_template='https://example.com/audio/%(book_no)s/%(chapter_no)s.mp3' name='Example KJV Audio' version='King James Version' version_abbr='KJV'
http --auth username:password POST http://127.0.0.1:2851/audiooffsets/ source:=1 verse:=123
http --auth username:password POST http://127.0.0.1:2851/verseranges/ selection:=1 start_verse:=10 end_verse:=25
```

---

## Notes for future work

- Add any extra endpoints or response fields only if the client contract requires them.
- If this API grows, consider a dedicated read schema for list/detail payloads so the internal model fields are explicit instead of implicit.
- Keep validation consistent across serializer and model layers when new relationship rules are introduced.
