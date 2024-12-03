function PageTemplate({ title, children }: { title: string; children?: React.ReactNode }) {
  return (
    <div className="h-screen w-screen flex items-center justify-center outer-page">
      <div className="w-[84rem] h-[55rem] main_window py-6 backdrop-blur-2xl flex flex-col items-center">
        <div>
          <span className="text-3xl tracking-[5px] text-[#fad053c0] font-bold uppercase">{title}</span>
        </div>
        <div className="w-full h-full flex flex-col items-center justify-center">{children}</div>
      </div>
    </div>
  );
}

export default PageTemplate;
