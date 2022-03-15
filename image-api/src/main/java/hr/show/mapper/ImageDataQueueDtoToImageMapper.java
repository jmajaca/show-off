package hr.show.mapper;

import hr.show.message.ImageDataQueueMessage;
import hr.show.model.Image;
import hr.show.model.ImageBox;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.LinkedList;
import java.util.List;

@Component
public class ImageDataQueueDtoToImageMapper {

    private final ImageBoxDataQueueDtoToImageBoxMapper imageBoxDataQueueDtoToImageBoxMapper;

    @Autowired
    public ImageDataQueueDtoToImageMapper(ImageBoxDataQueueDtoToImageBoxMapper imageBoxDataQueueDtoToImageBoxMapper) {
        this.imageBoxDataQueueDtoToImageBoxMapper = imageBoxDataQueueDtoToImageBoxMapper;
    }

    public Image map(ImageDataQueueMessage dto) {
        Image image = new Image();

        image.setId(dto.getId());
        image.setCreationTimestamp(LocalDateTime.now());

        List<ImageBox> boxes = new LinkedList<>();
        dto.getBox().forEach(imageBoxDataQueueDto -> boxes.add(imageBoxDataQueueDtoToImageBoxMapper.map(imageBoxDataQueueDto)));
        image.setBoxes(boxes);

        return image;
    }

}
