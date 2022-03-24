import React, {Dispatch, SetStateAction, useState} from 'react'

import {Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Slide, TextareaAutosize} from '@mui/material';
import {TransitionProps} from '@mui/material/transitions';
import {makeStyles} from '@mui/styles';

import {TextPopupData} from '../../pages/MainPage';
import CustomSnackbar from '../snackbars/CustomSnackbar';

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
    showSuccessSnackBar?: boolean,
    className?: string,
}

export default function TextPopup({open, text, title, setPopupData, showSuccessSnackBar = true, className}: TextPopupProps) {

    const [enableEdit, setEnableEdit] = useState<boolean>(true);
    const [openSnackbar, setOpenSnackbar] = useState<boolean>(false);

    const classes = useStyles();

    const ON_EDIT_MESSAGE = 'Text correction sent';

    const handleClose = () => {
        setPopupData({open: false, 'text': text});
        setEnableEdit(true);
        if (showSuccessSnackBar && !enableEdit) {
            setOpenSnackbar(true);
        }
    }

    const handleEdit = () => {
        setEnableEdit(false);
    }

    return (
        <>
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
                            disabled={enableEdit}
                            onChange={(e) => setPopupData({text: e.target.value, open: true})}
                        />
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    { enableEdit && <Button onClick={handleEdit}>Edit</Button>}
                    <Button onClick={handleClose}>OK</Button>
                </DialogActions>
            </Dialog>
            <CustomSnackbar open={openSnackbar} setOpen={setOpenSnackbar} type='success' message={ON_EDIT_MESSAGE} />
        </>
    );


}