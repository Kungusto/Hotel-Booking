docker network create myNetwork

docker run --name booking_db `
    -p 6432:5432 `
    -e POSTGRES_USER=abcde `
    -e POSTGRES_PASSWORD=abcde `
    -e POSTGRES_DB=bookings `
    --network=myNetwork `
    --volume pg-booking-data:/var/lib/postgresql/data `
    -d postgres:16

docker run --name booking_cache `
    -p 7379:6379 `
    --network=myNetwork `
    -d redis:7.4

docker run --name booking_back `
    -p 7777:8000 `
    --network=myNetwork `
    bookings_image

docker run --name celery_worker `
    --network=myNetwork `
    booking_image `
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO --pool=solo

docker run --name celery_beat `
    --network=myNetwork `
    booking_image `
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B --pool=solo

docker build -t bookings_image .    
