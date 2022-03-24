package hr.show.message;

import lombok.Data;

import javax.validation.constraints.NotEmpty;
import java.util.List;

@Data
public class ImageDataQueueMessage {

    @NotEmpty(message = "id is required")
    private String id;

    private List<ImageBoxDataQueueMessage> box;

    private String text;

}

