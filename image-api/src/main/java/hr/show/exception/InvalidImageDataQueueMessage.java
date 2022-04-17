package hr.show.exception;

public class InvalidImageDataQueueMessage extends RuntimeException {

    private static final String defaultErrorMessage = "Request id '%s' is not valid";

    public InvalidImageDataQueueMessage(String requestId, Throwable e) {
        super(String.format(defaultErrorMessage, requestId), e);
    }

    public InvalidImageDataQueueMessage(String requestId) {
        super(String.format(defaultErrorMessage, requestId));
    }

}
