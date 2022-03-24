package hr.show.message;

import lombok.Data;

import javax.validation.constraints.NotEmpty;

@Data
public class TextCorrectionQueueMessage {

    @NotEmpty(message = "id is required")
    private String id;

    private String text;

}
