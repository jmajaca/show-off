package hr.show.service;

import hr.show.message.ImageBoxDataQueueMessage;
import hr.show.dto.ImageDto;

import java.util.List;
import java.util.Optional;

public interface ImageService {

    void saveDataImage(List<ImageBoxDataQueueMessage> imageDataQueueMessage, String requestId);

    Optional<ImageDto> getImage(String imageId);

    void saveTextCorrection(String imageId, String value);

    void writeImage(byte[] image, String requestId);
}
