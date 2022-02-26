package hr.show.dto;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
@EqualsAndHashCode
@RequiredArgsConstructor
public class ImageBoxDto {

    private Integer startX;

    private Integer startY;

    private Integer width;

    private Integer height;

    private String text;

}
