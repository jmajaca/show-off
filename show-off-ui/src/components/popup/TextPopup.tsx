import React, {Dispatch, SetStateAction, useEffect, useState} from 'react'

import {Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Slide, TextareaAutosize} from '@mui/material';
import {TransitionProps} from '@mui/material/transitions';
import {makeStyles} from '@mui/styles';

import {TextPopupData} from '../../pages/MainPage';

const useStyles = makeStyles({
    textArea: {
        border: 'none',
        width: '100%',
        outline: 'none',
        resize: 'none',
        backgroundColor: 'transparent'
    },
});

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
    title: string,
    setPopupData: Dispatch<SetStateAction<TextPopupData>>,
    className?: string,
}

export default function TextPopup({open, text, title, setPopupData, className}: TextPopupProps) {

    const [disableEdit, setDisableEdit] = useState<boolean>(true);

    const classes = useStyles();

    const handleClose = () => {
        setPopupData({open: false, 'text': text})
    }

    const handleEdit = () => {
        setDisableEdit(false);
    }

    return (
        <Dialog
            open={open}
            TransitionComponent={Transition}
            keepMounted
            onClose={handleClose}
        >
            <DialogTitle>{title}</DialogTitle>
            <DialogContent>
                <DialogContentText>
                    <TextareaAutosize
                        value={text}
                        minRows={3}
                        className={classes.textArea}
                        disabled={disableEdit}
                        onChange={(e) => setPopupData({text: e.target.value, open: true})}
                    />
                </DialogContentText>
            </DialogContent>
            <DialogActions>
                { disableEdit && <Button onClick={handleEdit}>Edit</Button>}
                <Button onClick={handleClose}>OK</Button>
            </DialogActions>
        </Dialog>
    );


}