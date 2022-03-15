package hr.show.mapper;

import hr.show.message.ImageBoxDataQueueMessage;
import hr.show.model.ImageBox;
import org.springframework.stereotype.Component;

@Component
public class ImageBoxDataQueueDtoToImageBoxMapper {

    public ImageBox map(ImageBoxDataQueueMessage dto) {
        ImageBox imageBox = new ImageBox();
        imageBox.setStartX(dto.getStartX());
        imageBox.setStartY(dto.getStartY());
        imageBox.setHeight(dto.getHeight());
        imageBox.setWidth(dto.getWidth());
        return imageBox;
    }

}
