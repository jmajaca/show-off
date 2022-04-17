package hr.show.message;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.PositiveOrZero;

@Data
public class ImageBoxDataQueueMessage {

    @JsonProperty("start_x")
    @NotNull(message = "start x is required")
    @PositiveOrZero(message = "start x must be greater or equal to 0")
    private Integer startX;

    @JsonProperty("start_y")
    @NotNull(message = "start y is required")
    @PositiveOrZero(message = "start y must be greater or equal to 0")
    private Integer startY;

    @NotNull(message = "width is required")
    @PositiveOrZero(message = "width must be greater or equal to 0")
    private Integer width;

    @NotNull(message = "height is required")
    @PositiveOrZero(message = "height must be greater or equal to 0")
    private Integer height;

    private String text;

}
