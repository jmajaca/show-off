package hr.show.exception;

public class NoEntityException extends RuntimeException {

    private static final String defaultErrorMessage = "Entity %s not found for id %s";

    public NoEntityException(Class<?> entityClass, String entityId, Throwable e) {
        this(String.format(defaultErrorMessage, entityClass.getName(), entityId), e);
    }

    public NoEntityException(Class<?> entityClass, Long entityId, Throwable e) {
        this (entityClass, String.valueOf(entityId), e);
    }

    public NoEntityException(Class<?> entityClass, String entityId) {
        this(String.format(defaultErrorMessage, entityClass.getName(), entityId));
    }

    public NoEntityException(Class<?> entityClass, Long entityId) {
        this(entityClass, String.valueOf(entityId));
    }

    public NoEntityException(String errorMessage) {
        super(errorMessage);
    }

    public NoEntityException(String errorMessage, Throwable err) {
        super(errorMessage, err);
    }

}
