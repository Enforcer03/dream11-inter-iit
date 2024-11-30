function PageTemplateWithoutTop({ children }: { children?: React.ReactNode }) {
  return (
    <div className="h-screen w-screen flex items-center justify-center outer-page">
<<<<<<< Updated upstream
      <div className="w-[89rem] h-[59rem] main_window_without_top py-10 backdrop-blur-2xl flex flex-col items-center">
        <div className="w-full h-full flex flex-col items-center justify-center">{children}</div>
      </div>
=======
      <div className="w-[83rem] h-[55rem] main_window_without_top py-10 backdrop-blur-2xl flex flex-col items-center"></div>
>>>>>>> Stashed changes
    </div>
  );
}

export default PageTemplateWithoutTop;
