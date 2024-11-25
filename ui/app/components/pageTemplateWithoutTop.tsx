export default function PageTemplateWithoutTop({ children }: { children?: React.ReactNode }) {
  return (
    <div className="h-screen w-screen flex items-center justify-center outer-page">
      <div className="w-4/6 h-5/6 main_window_without_top py-10 flex flex-col items-center">
        <div className="w-full h-full flex flex-col items-center justify-center">{children}</div>
      </div>
    </div>
  );
}
