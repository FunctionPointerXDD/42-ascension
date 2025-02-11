#!/bin/bash

## 임시로 토큰 발행해서 db에 유저 생성
ACCESS_TOKENS=()

NAMES=('Smith' 'Johnson' 'Williams' 'Brown' 'Jones' 'Miller' 'Davis' 'Garcia' 'Taylor' 'Anderson')

for i in {1..10}
do
    curl -X POST -H "Content-Type:application/json" -d "{\"user_id\":\"$i\"}" http://127.0.0.1:8100/jwt/user #-v
    echo ''
    sleep 1
    token=$(curl -X POST -H "Content-Type:application/json" -d "{\"user_id\":\"$i\"}" http://127.0.0.1:8100/jwt/new | jq -r '.access_token')
    echo "ACCESS_TOKEN: $token" >> 'token.txt'

    ACCESS_TOKENS+=("$token")

    echo "/user GET request ->"
    curl -X GET "http://127.0.0.1:8300/user/?user_name=${NAMES[$((i - 1))]}" \
         -H "Authorization: Bearer ${ACCESS_TOKENS[$((i - 1))]}"
    echo ''
done

echo "/user PUT request ->"
curl -X PUT "http://127.0.0.1:8300/user/" \
        -H "Authorization: Bearer ${ACCESS_TOKENS[0]}" \
        -H "Content-Type: application/json" -d '{"memo":"hello django~~~!"}'
echo ''

for ((i = 0; i < 10; i++))
do
    echo "/user/friend POST request ->"
    curl -X POST "http://127.0.0.1:8300/user/friend" \
         -H "Authorization: Bearer ${ACCESS_TOKENS[0]}" \
         -H "Content-Type: application/json" -d "{\"user_name\":\"${NAMES[$i]}\"}"
    echo ''
done

echo "/user/friend GET request ->"
curl -X GET "http://127.0.0.1:8300/user/friend" \
        -H "Authorization: Bearer ${ACCESS_TOKENS[0]}"
echo ''


# curl -X POST -H "Content-Type:application/json"  \
#      -d '{"player1_id":"1", "player2_id":"2", "player1_score":"3", "player2_score":"2", "winner_id":"1", "match_date":"2025-02-10T14:30:00Z", "play_time": "50"}' \
#          http://127.0.0.1:8300/_internal/dashboard

### 게임 서버로 부터 받는 POST요청 시뮬레이터 ###

# 2025년 전체 범위 내에서 랜덤한 match_date를 생성하기 위한 epoch 범위 (UTC 기준)
start_epoch=$(date -u -d "2025-01-01T00:00:00Z" +%s)
end_epoch=$(date -u -d "2025-12-31T23:59:59Z" +%s)

# 요청할 URL
url="http://127.0.0.1:8300/_internal/dashboard"

# 20회 반복
for i in {1..20}; do
  player1_id=$(shuf -i 1-10 -n 1)
  player2_id=$(shuf -i 1-10 -n 1)

  if [ $((RANDOM % 2)) -eq 0 ]; then
      winner_id=$player1_id
  else
      winner_id=$player2_id
  fi

  player1_score=$(shuf -i 0-5 -n 1)
  player2_score=$(shuf -i 0-5 -n 1)
  play_time=$(shuf -i 0-600 -n 1)

  # 랜덤한 epoch 생성 후 UTC ISO 8601 형식으로 변환 (ex: "2025-02-10T14:30:00Z")
  random_epoch=$(shuf -i ${start_epoch}-${end_epoch} -n 1)
  match_date=$(date -u -d @"$random_epoch" +"%Y-%m-%dT%H:%M:%SZ")

  # JSON payload 생성 (여기서는 모든 값을 문자열로 전송합니다)
  payload=$(cat <<EOF
{
  "player1_id": "$player1_id",
  "player2_id": "$player2_id",
  "player1_score": "$player1_score",
  "player2_score": "$player2_score",
  "winner_id": "$winner_id",
  "match_date": "$match_date",
  "play_time": "$play_time"
}
EOF
)

  echo "Sending request $i:"
  echo "$payload"
  curl -X POST -H "Content-Type:application/json" -d "$payload" "$url"
  echo -e "\n"
done

### 게임 시뮬레이터 종료 ###

#curl -X PUT -F "image_url=@/home/kapustin/tsen/backend/backend/mice.png" -F "user_name=chansjeo" -H "Authorization: Bearer <token>" http://127.0.0.1:8300/user/

echo ''
for ((i = 0; i < 10; i++))
do
    echo "/user/dashboard GET request ->"
    curl -X POST "http://127.0.0.1:8300/user/dashboard" \
         -H "Authorization: Bearer ${ACCESS_TOKENS[0]}" >> dashboard.json
    echo ''
done