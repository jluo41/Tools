/* Public surface of the console — what an embedder imports.
 *
 * The REACH D01 demo consumes exactly this (via a Vite alias), so the demo and
 * the HAI-Chat panel can never drift apart.
 */
export {default as Console} from './Console';
export {default as AnnotateView} from './components/AnnotateView';
export {default as ExternalView} from './components/ExternalView';
export {default as HaiChatDrawer} from './components/HaiChatDrawer';
export {default as HealthView} from './components/HealthView';
export {default as InternalView} from './components/InternalView';
export {default as ModelCard} from './components/ModelCard';
export {default as ModelPicker} from './components/ModelPicker';
export {default as NavRail} from './components/NavRail';
export {default as PatientCard} from './components/PatientCard';
export {default as PatientChart} from './components/PatientChart';
export {default as PatientCombobox} from './components/PatientCombobox';
export {default as PatientRoster} from './components/PatientRoster';
export {default as RawDataPanel} from './components/RawDataPanel';
export {default as RawFilesPanel} from './components/RawFilesPanel';
export {default as RecordPanel} from './components/RecordPanel';
export {default as RunsPanel} from './components/RunsPanel';
export {default as Splitter} from './components/Splitter';
export {default as TabStrip} from './components/TabStrip';
export * from './views';
export {useConsole} from './useConsole';
export * from './types';
