# Running this app

Prerequisites: docker and docker-compose.

To run the server, execute 

```bash
docker-compose up -d
```

from the top-level directory containing the `docker-compose.yaml` file and navigate to [`http://localhost:8080`](http://localhost:8080) to access the API and GraphiQL interface.

The docker-compose command will

* start a MongoDB instance
* load the `init` service, which loads initialization data from `data/rivm2016.csv` into MongoDB (if it has not been loaded before)
* start a GraphQL server
* start a NGINX server that exposes the GraphQL API on port `8080`

The `init` service will initialize the database with the data found in `data/rivm2016.csv`.
If the database has already been initialized, this step will be skipped.

The database can be re-initialized manually by setting the `--force` flag on the script run by `init`.
This will empty the database and re-load the data.

You can also run the initialization script manually, provided that the MongoDB container is running:

```bash
cd init/src
PYTHONPATH=mblib/src MONGODB_HOST=localhost DATA_PATH="data/rivm2016.csv" python init/src/main.py
```
