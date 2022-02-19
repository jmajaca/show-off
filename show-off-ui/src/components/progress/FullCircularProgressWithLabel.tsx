import CircularProgressWithLabel from './CircularProgressWithLabel';
import {CircularProgress} from '@mui/material';
import {makeStyles} from '@mui/styles';

const useStyles = makeStyles({
    active: {
        zIndex: 1001,
        position: 'relative',
    },
    static: {
        zIndex: 900,
        position: 'absolute', // this should be relative to current component
        top: '50%',
        //position: 'relative',
        //marginTop: '-86%'
    },
})

type FullCircularProgressWithLabelProps = {
    value: number,
    className?: string,
}

export default function FullCircularProgressWithLabel({value, className}: FullCircularProgressWithLabelProps) {

    const classes = useStyles();

    return (
        <div className={className}>
            <CircularProgressWithLabel value={value} className={classes.active}/>
            <CircularProgress variant="determinate" style={{color: 'grey'}} className={classes.static} value={100} thickness={5} size={80}/>
        </div>
    );
    
}