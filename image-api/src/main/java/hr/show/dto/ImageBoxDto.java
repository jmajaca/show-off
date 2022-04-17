package hr.show.dto;

import lombok.Data;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.PositiveOrZero;

/**
 * Image Box Dto
 * @author jmajaca
 * */
@Data
public class ImageBoxDto {

    @NotNull(message = "start x is required")
    @PositiveOrZero(message = "start x must be greater or equal to 0")
    private Integer startX;

    @NotNull(message = "start y is required")
    @PositiveOrZero(message = "start y must be greater or equal to 0")
    private Integer startY;

    @NotNull(message = "width is required")
    @PositiveOrZero(message = "width must be greater or equal to 0")
    private Integer width;

    @NotNull(message = "height is required")
    @PositiveOrZero(message = "height must be greater or equal to 0")
    private Integer height;

    @NotEmpty(message = "text must not be empty")
    private String text;

}
