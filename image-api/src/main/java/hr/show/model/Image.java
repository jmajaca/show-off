package hr.show.model;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.Hibernate;

import javax.persistence.*;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Objects;

@Getter
@Setter
@ToString
@RequiredArgsConstructor
@Entity
public class Image {

    @Id
    @Column(name = "id", length = 36, nullable = false)
    private String id;

    @Column(name = "path", nullable = false)
    private String path;

    @Column(name = "creation_timestamp", nullable = false)
    private LocalDateTime creationTimestamp;

    @OneToMany(mappedBy="image", cascade = CascadeType.REFRESH)
    @ToString.Exclude
    private List<ImageBox> boxes;

    @OneToOne(mappedBy="image", cascade = CascadeType.REFRESH)
    private TextCorrection textCorrection;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o)) return false;
        Image image = (Image) o;
        return id != null && Objects.equals(id, image.id);
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}
