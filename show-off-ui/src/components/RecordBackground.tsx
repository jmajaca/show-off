import React from 'react';


type RecordBackgroundProps = {
    className?: string,
}

export default function RecordBackground({className}: RecordBackgroundProps) {

    return (
        <div className={className}>
            <input type="file" accept="image/*" capture="environment"/>
        </div>
    );

}