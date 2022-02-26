package hr.show.service.impl;

import hr.show.dto.ImageDto;
import hr.show.exception.NoEntityException;
import hr.show.model.Image;
import hr.show.model.TextCorrection;
import hr.show.repository.ImageRepository;
import hr.show.repository.TextCorrectionRepository;
import hr.show.service.ImageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class ImageServiceImpl implements ImageService {

    private final ImageRepository imageRepository;
    private final TextCorrectionRepository textCorrectionRepository;

    @Autowired
    public ImageServiceImpl(ImageRepository imageRepository, TextCorrectionRepository textCorrectionRepository) {
        this.imageRepository = imageRepository;
        this.textCorrectionRepository = textCorrectionRepository;
    }

    @Override
    public void saveImage(ImageDto imageDto) {
        // save file to file system
        String path = "mock";
        // map
        Image image = new Image();
        image.setId(imageDto.getId());
        image.setCreationTimestamp(imageDto.getCreationDate());
        image.setPath(path);
        // save to db
        imageRepository.saveAndFlush(image);
    }

    @Override
    public Optional<ImageDto> getImage(String imageId) {
        throw new NoEntityException(Image.class, imageId);
    }

    @Override
    public void saveTextCorrection(String imageId, String value) {
        TextCorrection textCorrection = new TextCorrection();
        textCorrection.setValue(value);
        textCorrection.setImage(imageRepository.getById(imageId));
        textCorrectionRepository.saveAndFlush(textCorrection);
    }
}
