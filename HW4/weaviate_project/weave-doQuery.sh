echo '{
  "query": "{
    Get{
      SimSearch (
        limit: 1
        nearText: {
          concepts: [\"Marine\"],
        }
      ){
        course_name
        course_desc
        school
      }
    }
  }"
}'  | curl \
    -X POST \
    -H 'Content-Type: application/json' \
    -d @- \
    localhost:8080/v1/graphql
