package hr.show.dto;

import lombok.Data;

import javax.validation.constraints.NotEmpty;

/**
 * Text Correction Dto
 * @author jmajaca
 * */
@Data
public class TextCorrectionDto {

    @NotEmpty(message = "value is required")
    private String value;

    @NotEmpty(message = "image id is required")
    private String imageId;

}
