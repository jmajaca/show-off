package hr.show.job;

import hr.show.configuration.FileProperties;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class ImageDeleteJob {

    private static Logger log = LoggerFactory.getLogger(ImageDeleteJob.class);

    private final String imageDirPath;

    private final Integer imageMaxAge;

    public ImageDeleteJob(FileProperties fileProperties) {
        this.imageDirPath = fileProperties.getPath();
        this.imageMaxAge = fileProperties.getMaxAge();
    }

    @Scheduled(cron = "0 15 0 * * *")
    public void deleteImageDir() {
        // TODO implement
    }

}
