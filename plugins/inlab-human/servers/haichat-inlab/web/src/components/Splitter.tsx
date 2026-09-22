/* Splitter — a draggable divider.
 *
 * Reports a delta in px while dragging; the parent decides what to resize.
 * Works for both vertical dividers (resizing widths) and horizontal ones
 * (resizing heights), so one component covers every seam in the layout.
 *
 * Source of truth lives here, in HAI-Chat. The REACH D01 demo imports it from
 * this folder rather than keeping a copy — one component, no fork.
 */
import {useCallback, useEffect, useRef} from 'react';

interface Props {
    /** 'vertical' = a vertical bar you drag left/right (resizes width). */
    orientation: 'vertical' | 'horizontal';
    onDrag: (deltaPx: number) => void;
    onDoubleClick?: () => void;
}

export default function Splitter({orientation, onDrag, onDoubleClick}: Props) {
    const dragging = useRef(false);
    const last = useRef(0);
    const vertical = orientation === 'vertical';

    const onMove = useCallback(
        (e: MouseEvent) => {
            if (!dragging.current) {
                return;
            }
            const pos = vertical ? e.clientX : e.clientY;
            onDrag(pos - last.current);
            last.current = pos;
        },
        [onDrag, vertical],
    );

    const onUp = useCallback(() => {
        dragging.current = false;
        document.body.style.cursor = '';
        document.body.style.userSelect = '';
    }, []);

    useEffect(() => {
        window.addEventListener('mousemove', onMove);
        window.addEventListener('mouseup', onUp);
        return () => {
            window.removeEventListener('mousemove', onMove);
            window.removeEventListener('mouseup', onUp);
        };
    }, [onMove, onUp]);

    return (
        <div
            className={'splitter ' + orientation}
            onDoubleClick={onDoubleClick}
            onMouseDown={(e) => {
                dragging.current = true;
                last.current = vertical ? e.clientX : e.clientY;
                // keep the cursor + kill text selection for the whole drag
                document.body.style.cursor = vertical ? 'col-resize' : 'row-resize';
                document.body.style.userSelect = 'none';
            }}
        />
    );
}
