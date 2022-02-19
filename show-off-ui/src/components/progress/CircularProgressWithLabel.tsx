import {Box, CircularProgress, CircularProgressProps, Typography} from '@mui/material';
import {makeStyles} from '@mui/styles';

const useStyles = makeStyles({
    label: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    labelWrapper: {
        marginTop: '-85%',
    }
})

export default function CircularProgressWithLabel(props: CircularProgressProps & { value: number }) {

    const classes = useStyles();

    return (
        <Box>
            <CircularProgress variant="determinate" thickness={5} size={80} {...props} />
            <Box className={classes.labelWrapper}>
                <Typography variant="caption" component="div" color="primary" fontSize={30} fontWeight={600} className={classes.label}>
                    {Math.round(props.value)}
                </Typography>
            </Box>
        </Box>
    );
}