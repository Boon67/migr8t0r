docker-compose -f "docker-compose.yml" down
docker-compose -f "docker-compose.yml" up -d --build

python3 -m pip install -r ./requirements.txt --user
echo 'Waiting for Environment to Initialize (its mysqls fault) 300 seconds........'
sleep 300
echo 'The wait is over'
echo 'Running migration....'
python3 main.py
echo 'Migration complete'