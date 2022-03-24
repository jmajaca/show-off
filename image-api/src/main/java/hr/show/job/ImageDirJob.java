package hr.show.job;

import hr.show.configuration.FileProperties;
import hr.show.util.ImageUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.io.File;
import java.util.concurrent.TimeUnit;

@Component
public class ImageDirJob {

    private static final Logger log = LoggerFactory.getLogger(ImageDirJob.class);

    private final String imageDirPath;

    public ImageDirJob(FileProperties fileProperties) {
        imageDirPath = fileProperties.getPath();
    }

    @Scheduled(cron = "0 55 23 * * *")
    public void createImageDir() throws InterruptedException {
        String dirPath = ImageUtil.joinDirAndFilePaths(imageDirPath, ImageUtil.getCurrentDayDirName());
        File appDataDir = new File(dirPath);
        boolean success = appDataDir.mkdirs();
        while (!success) {
            TimeUnit.SECONDS.sleep(10);
            success = appDataDir.mkdirs();
        }
        log.info("Created image dir {}", dirPath);
    }

}
