import React from 'react'

import {Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Slide} from '@mui/material';
import {TransitionProps} from '@mui/material/transitions';

const Transition = React.forwardRef(function Transition(
    props: TransitionProps & {
        children: React.ReactElement<any, any>;
    },
    ref: React.Ref<unknown>,
) {
    return <Slide direction="up" ref={ref} {...props}/>;
});

type TextPopupProps = {
    open: boolean,
    text: string,
    handleClose?: (affirmative: boolean) => void,
}

export default function TextPopup({open, text, handleClose}: TextPopupProps) {

    const handleAffirmativeClose = () => {
        if (handleClose) {
            handleClose(true);
        }
    }

    const handleNonAffirmativeClose = () => {
        if (handleClose) {
            handleClose(false);
        }
    }

    return (
        <Dialog
            open={open}
            TransitionComponent={Transition}
            keepMounted
            onClose={handleClose}
        >
            <DialogTitle>{"Title placeholder"}</DialogTitle>
            <DialogContent>
                <DialogContentText>
                    {text}
                </DialogContentText>
            </DialogContent>
            <DialogActions>
                <Button onClick={handleNonAffirmativeClose}>Disagree</Button>
                <Button onClick={handleAffirmativeClose}>Agree</Button>
            </DialogActions>
        </Dialog>
    );


}