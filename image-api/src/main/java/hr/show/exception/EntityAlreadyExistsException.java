package hr.show.exception;

public class EntityAlreadyExistsException extends RuntimeException {

    private static final String defaultErrorMessage = "Entity %s exists for id %d";

    public EntityAlreadyExistsException(Class<?> entityClass, Long entityId, Throwable e) {
        this(String.format(defaultErrorMessage, entityClass.getName(), entityId), e);
    }

    public EntityAlreadyExistsException(Class<?> entityClass, Long entityId) {
        this(String.format(defaultErrorMessage, entityClass.getName(), entityId));
    }

    public EntityAlreadyExistsException(String errorMessage) {
        super(errorMessage);
    }

    public EntityAlreadyExistsException(String errorMessage, Throwable err) {
        super(errorMessage, err);
    }

}
