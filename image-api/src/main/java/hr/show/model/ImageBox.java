package hr.show.model;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.Hibernate;

import javax.persistence.*;
import java.util.Objects;

@Getter
@Setter
@ToString
@RequiredArgsConstructor
@Entity
public class ImageBox {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private Long id;

    @Column(name = "start_x", nullable = false)
    private Integer startX;

    @Column(name = "start_y", nullable = false)
    private Integer startY;

    @Column(name = "width", nullable = false)
    private Integer width;

    @Column(name = "height", nullable = false)
    private Integer height;

    @Column(name = "text", length = 512, nullable = false)
    private String text;

    @ManyToOne
    @JoinColumn(name="image_id", nullable=false)
    private Image image;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o)) return false;
        ImageBox imageBox = (ImageBox) o;
        return id != null && Objects.equals(id, imageBox.id);
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}
