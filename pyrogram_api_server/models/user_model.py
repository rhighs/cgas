success_key = "isSuccess"
data_key = "data"
message_key = "message"

class UserModels:
    @staticmethod
    def success(message=None, data=None):
        if message != None and data != None:
            return {
                success_key : True,
                message_key : message,
                data_key : data
            }
        elif message != None:
            return {
                success_key : True,
                message_key : message,
            }
        return {
            success_key : True,
            data_key : data,
        }

    @staticmethod
    def failure(message=None):
        if message != None:
            return {
                success_key: False
            }
        return {
            success_key: False,
            message_key: message
        }

