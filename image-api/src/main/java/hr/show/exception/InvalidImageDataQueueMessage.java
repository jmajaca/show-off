package hr.show.exception;

public class InvalidImageDataQueueMessage extends RuntimeException {

    private static final String defaultErrorMessage = "Id from body '%s' does not match id from header '%s'";

    public InvalidImageDataQueueMessage(String bodyId, String requestId, Throwable e) {
        this(String.format(defaultErrorMessage, bodyId, requestId), e);
    }

    public InvalidImageDataQueueMessage(String bodyId, String requestId) {
        this(String.format(defaultErrorMessage, bodyId, requestId));
    }

    public InvalidImageDataQueueMessage(String errorMessage) {
        super(errorMessage);
    }

    public InvalidImageDataQueueMessage(String errorMessage, Throwable err) {
        super(errorMessage, err);
    }


}
