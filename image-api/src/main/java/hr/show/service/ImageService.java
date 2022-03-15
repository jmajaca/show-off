package hr.show.service;

import hr.show.message.ImageDataQueueMessage;
import hr.show.dto.ImageDto;

import java.util.Optional;

public interface ImageService {

    void saveDataImage(ImageDataQueueMessage imageDataQueueMessage);

    Optional<ImageDto> getImage(String imageId);

    void saveTextCorrection(String imageId, String value);

    void writeImage(byte[] image, String requestId);
}
