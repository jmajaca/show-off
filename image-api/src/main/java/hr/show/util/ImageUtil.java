package hr.show.util;

import java.text.SimpleDateFormat;
import java.util.Date;

public class ImageUtil {

    private final static SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yy-MM-dd");

    private final static String pathSeparator = "/";

    public static String getCurrentDayDirName() {
        return simpleDateFormat.format(new Date());
    }

    public static String joinDirAndFilePaths(String ...elements) {
       return String.join(pathSeparator, elements);
    }

}
