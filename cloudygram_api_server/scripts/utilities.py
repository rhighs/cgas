import json
from pyramid.response import Response

def jres(model, status):
    return Response(json.dumps(model),
                    charset="UTF-8",
                    content_type="application/json",
                    status=status)
