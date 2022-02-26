package hr.show.dto;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;

import java.io.File;
import java.time.LocalDateTime;
import java.util.List;

@Getter
@Setter
@ToString
@EqualsAndHashCode
@RequiredArgsConstructor
public class ImageDto {

    private String id;

    private File file;

    private LocalDateTime creationDate;

    private List<ImageBoxDto> boxes;

    private String textCorrection;

}
