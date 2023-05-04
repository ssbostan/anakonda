from anakonda.config import Config

STATUS_MESSAGES = {
    100: "OK",
    101: "Method is not implemented",
    102: "Schema validation failed",
    103: "Schema instance error",
    104: "Invalid input provided",
    105: "Media type is not supported",
    106: "Database error",
    107: "Resource not found",
    108: "Runtime not available",
    109: "Resource not updatable",
}


def jsonify(state={}, metadata={}, status=200, code=100, headers={}):
    resource = {}
    resource["result"] = state
    resource["metadata"] = metadata
    resource["status"] = {"code": code}
    if Config.DEBUG is True:
        resource["status"]["message"] = STATUS_MESSAGES[code]
    return resource, status, headers
