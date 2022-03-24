package hr.show.advice;

import hr.show.exception.EntityAlreadyExistsException;
import hr.show.exception.NoEntityException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.validation.ObjectError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.context.request.WebRequest;

import java.util.Arrays;
import java.util.Objects;
import java.util.stream.Collectors;

@ControllerAdvice
class GlobalControllerExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(GlobalControllerExceptionHandler.class);

    @ResponseStatus(HttpStatus.NOT_FOUND)
    @ExceptionHandler(NoEntityException.class)
    public void handleNoEntityException(NoEntityException exception, WebRequest request) {
        log.warn(exception.getMessage());
    }

    @ResponseStatus(HttpStatus.CONFLICT)
    @ExceptionHandler(EntityAlreadyExistsException.class)
    public void handleEntityAlreadyExistsException(EntityAlreadyExistsException exception) {
        log.warn(exception.getMessage());
    }


    // this overrides org.springframework.web.servlet.mvc.support.DefaultHandlerExceptionResolver
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public void handleMethodArgumentNotValidException(MethodArgumentNotValidException exception) {
        StringBuilder message = new StringBuilder();
        for(ObjectError error: exception.getBindingResult().getAllErrors()) {
            message.append("Field error in '").append(Arrays.stream(Objects.requireNonNull(error.getCodes())[0].split("\\.")).skip(1).collect(Collectors.joining(".")))
                    .append("' with message: '").append(error.getDefaultMessage()).append("'");
            message.append(", ");
        }
        message.setLength(message.length() - 2);
        log.warn(message.toString());
    }
}
