#!/bin/bash
echo "start support_create_project.sh waiting for 17 seconds..."
sleep 17
echo "start support_create_project.sh create dummy project"
curl -X POST -H "Content-Type: application/json" -d '{"project_name": "dummy"}' http://devika-backend:1337/api/create-project

# シェルを起動
exec /bin/bash
