## Run

Create .env file based on the .env.example file.
Run:
```bash
docker-compose build
docker-compose up
```
Service will be available on default localhost:8000 address.

## Testing

Send GET request on `/get_tasks/?build={build_name}` endpoint, where {build_name}
should be replaced with the actual build name the tasks should be provided for.
The result will be sorted accordingly.
