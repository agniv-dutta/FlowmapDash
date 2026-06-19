from flask import jsonify


class AppError(Exception):
    status_code = 500
    message = "Internal server error"
    details = None

    def __init__(self, message=None, status_code=None, details=None):
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code
        self.details = details
        super().__init__(self.message)

    def to_dict(self):
        payload = {"error": self.message}
        if self.details:
            payload["details"] = self.details
        return payload


class ValidationError(AppError):
    status_code = 400

    def __init__(self, message="Validation failed", details=None):
        super().__init__(message=message, details=details)


class NotFoundError(AppError):
    status_code = 404

    def __init__(self, message="Resource not found", details=None):
        super().__init__(message=message, details=details)


class RateLimitError(AppError):
    status_code = 429

    def __init__(self, message="Too many requests"):
        super().__init__(message=message)


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify(error.to_dict()), error.status_code

    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(405)
    def handle_405(error):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(400)
    def handle_400(error):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(500)
    def handle_500(error):
        if app.debug:
            import traceback
            return jsonify({"error": "Internal server error", "traceback": traceback.format_exc()}), 500
        return jsonify({"error": "Internal server error"}), 500

    @app.errorhandler(Exception)
    def handle_unhandled(error):
        app.logger.exception("Unhandled exception")
        if app.debug:
            import traceback
            return jsonify({"error": str(error), "traceback": traceback.format_exc()}), 500
        return jsonify({"error": "Internal server error"}), 500
