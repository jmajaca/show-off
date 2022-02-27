package hr.show.dto;

import lombok.Data;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import java.awt.image.BufferedImage;
import java.time.LocalDateTime;
import java.util.List;

/**
 * Image Dto
 * @author jmajaca
 * */
@Data
public class ImageDto {

    @NotEmpty(message = "id is required")
    private String id;

    @NotNull(message = "file must not be null")
    private BufferedImage file;

    @NotNull(message = "creation date must not be null")
    private LocalDateTime creationDate;

    private List<ImageBoxDto> boxes;

    private String textCorrection;

}
