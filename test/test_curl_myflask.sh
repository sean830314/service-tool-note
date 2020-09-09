for ip in $(seq 1 100)
do
  curl localhost:5000/update
  value=`shuf -i 1-10 -n 1`
  sleep $value
done
