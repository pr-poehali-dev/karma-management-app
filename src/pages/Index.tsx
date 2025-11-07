import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import Icon from '@/components/ui/icon';

const Index = () => {
  const [scrolled, setScrolled] = useState(false);
  const [seedGrowth, setSeedGrowth] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setSeedGrowth(prev => (prev + 1) % 8);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const scrollToSection = (id: string) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  };

  const features = [
    {
      icon: 'Target',
      title: 'Постановка целей',
      description: 'Определите свои истинные желания и создайте план их достижения'
    },
    {
      icon: 'Users',
      title: 'Поиск партнёров',
      description: 'Найдите единомышленников для совместного духовного роста'
    },
    {
      icon: 'Heart',
      title: 'Поле заслуг',
      description: 'Визуализируйте свои добрые дела и их влияние на мир'
    },
    {
      icon: 'Sparkles',
      title: 'Семя намерения',
      description: 'Посадите семя своей цели и наблюдайте за его ростом'
    }
  ];

  const plans = [
    {
      name: 'Росток',
      price: 'Бесплатно',
      features: ['Постановка 3 целей', 'Базовая визуализация', 'Доступ к сообществу']
    },
    {
      name: 'Цветение',
      price: '990₽/мес',
      features: ['Неограниченные цели', 'Расширенная визуализация', 'Поиск наставника', 'Аналитика прогресса'],
      popular: true
    },
    {
      name: 'Лотос',
      price: '2490₽/мес',
      features: ['Все функции Цветения', 'Персональный коуч', 'Закрытые мероприятия', 'Приоритетная поддержка']
    }
  ];

  const testimonials = [
    {
      name: 'Анна С.',
      text: 'Приложение помогло мне увидеть свой прогресс. Визуализация роста семени мотивирует каждый день!'
    },
    {
      name: 'Михаил К.',
      text: 'Нашёл здесь не только инструменты для работы над собой, но и поддержку единомышленников.'
    },
    {
      name: 'Елена П.',
      text: 'Поле заслуг показывает, как маленькие добрые дела создают большие изменения. Невероятно!'
    }
  ];

  const faqs = [
    {
      question: 'Что такое кармический менеджмент?',
      answer: 'Это система осознанного управления своими действиями, намерениями и энергией для достижения гармонии и целей.'
    },
    {
      question: 'Как работает визуализация семени?',
      answer: 'Вы "сажаете" семя своей цели, поливаете его ежедневными действиями, и наблюдаете визуальный рост по мере прогресса.'
    },
    {
      question: 'Можно ли использовать бесплатно?',
      answer: 'Да! План "Росток" бесплатен и включает основные функции для начала вашего пути.'
    },
    {
      question: 'Как найти партнёров и наставников?',
      answer: 'В приложении есть раздел сообщества, где вы можете найти людей с похожими целями и интересами.'
    }
  ];

  return (
    <div className="min-h-screen">
      <nav className={`fixed top-0 w-full z-50 transition-all duration-300 ${scrolled ? 'bg-white/90 backdrop-blur-md shadow-md' : 'bg-transparent'}`}>
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-primary">KarmaFlow</h1>
          <div className="hidden md:flex gap-6">
            {['hero', 'features', 'visualization', 'pricing', 'testimonials', 'faq', 'contact'].map((section) => (
              <button
                key={section}
                onClick={() => scrollToSection(section)}
                className="text-foreground/70 hover:text-primary transition-colors capitalize"
              >
                {section === 'hero' ? 'Главная' : 
                 section === 'features' ? 'Возможности' :
                 section === 'visualization' ? 'Визуализация' :
                 section === 'pricing' ? 'Тарифы' :
                 section === 'testimonials' ? 'Отзывы' :
                 section === 'faq' ? 'FAQ' : 'Контакты'}
              </button>
            ))}
          </div>
        </div>
      </nav>

      <section id="hero" className="pt-32 pb-20 px-4 bg-gradient-to-b from-accent/30 to-background">
        <div className="container mx-auto text-center">
          <h2 className="text-5xl md:text-6xl font-bold mb-6 animate-fade-in">
            Управляй своей кармой
          </h2>
          <p className="text-xl md:text-2xl text-muted-foreground mb-8 animate-fade-in" style={{ animationDelay: '0.2s' }}>
            Визуализируй цели, выращивай намерения, создавай своё будущее
          </p>
          <div className="flex gap-4 justify-center animate-fade-in" style={{ animationDelay: '0.4s' }}>
            <Button size="lg" className="text-lg px-8" onClick={() => scrollToSection('pricing')}>
              Начать путь
            </Button>
            <Button size="lg" variant="outline" className="text-lg px-8" onClick={() => scrollToSection('visualization')}>
              Узнать больше
            </Button>
          </div>
          <div className="mt-16 animate-float">
            <img 
              src="https://cdn.poehali.dev/projects/fea94c96-848b-4380-9581-bae89ae561e0/files/b12ad071-2550-4296-87e4-a8cd41b12163.jpg" 
              alt="Медитация" 
              className="mx-auto rounded-3xl shadow-2xl max-w-2xl w-full"
            />
          </div>
        </div>
      </section>

      <section id="features" className="py-20 px-4">
        <div className="container mx-auto">
          <h2 className="text-4xl font-bold text-center mb-4">Возможности приложения</h2>
          <p className="text-center text-muted-foreground mb-12 text-lg">Инструменты для вашего духовного роста</p>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow animate-fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
                <CardHeader>
                  <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                    <Icon name={feature.icon as any} className="text-primary" size={24} />
                  </div>
                  <CardTitle>{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">{feature.description}</CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      <section id="visualization" className="py-20 px-4 bg-gradient-to-b from-secondary/20 to-background">
        <div className="container mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold mb-6">Визуализация роста</h2>
              <p className="text-lg text-muted-foreground mb-6">
                Посадите семя своего намерения и наблюдайте, как оно растёт с каждым вашим действием. 
                Поливайте его ежедневной практикой, и оно превратится в цветущее дерево достижений.
              </p>
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <Icon name="Droplet" className="text-primary" />
                  <span>Ежедневный полив — маленькие шаги к цели</span>
                </div>
                <div className="flex items-center gap-3">
                  <Icon name="Sprout" className="text-primary" />
                  <span>Еженедельная посадка новых семян</span>
                </div>
                <div className="flex items-center gap-3">
                  <Icon name="TreePine" className="text-primary" />
                  <span>Наблюдение за ростом вашего сада целей</span>
                </div>
              </div>
            </div>
            <div className="relative">
              <div className="bg-gradient-to-br from-primary/20 to-secondary/20 rounded-3xl p-8 h-96 flex items-center justify-center">
                <img 
                  src="https://cdn.poehali.dev/projects/fea94c96-848b-4380-9581-bae89ae561e0/files/35699bdf-a56c-43c2-b23f-3bd5466f6990.jpg" 
                  alt="Рост семени" 
                  className="max-h-full animate-grow"
                  style={{ animationDelay: `${seedGrowth * 0.3}s` }}
                />
              </div>
              <div className="absolute -bottom-4 -right-4 bg-white rounded-2xl p-4 shadow-lg">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse"></div>
                  <span className="text-sm font-medium">Активный рост</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="pricing" className="py-20 px-4">
        <div className="container mx-auto">
          <h2 className="text-4xl font-bold text-center mb-4">Выберите свой путь</h2>
          <p className="text-center text-muted-foreground mb-12 text-lg">Начните с бесплатного плана или ускорьте рост</p>
          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {plans.map((plan, index) => (
              <Card 
                key={index} 
                className={`relative hover:shadow-xl transition-all ${plan.popular ? 'border-primary border-2 scale-105' : ''}`}
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-primary text-white px-4 py-1 rounded-full text-sm font-medium">
                    Популярный
                  </div>
                )}
                <CardHeader>
                  <CardTitle className="text-2xl">{plan.name}</CardTitle>
                  <div className="text-3xl font-bold mt-2">{plan.price}</div>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-3 mb-6">
                    {plan.features.map((feature, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <Icon name="Check" className="text-primary mt-1 flex-shrink-0" size={18} />
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>
                  <Button className="w-full" variant={plan.popular ? 'default' : 'outline'}>
                    {plan.price === 'Бесплатно' ? 'Попробовать' : 'Выбрать план'}
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      <section id="testimonials" className="py-20 px-4 bg-gradient-to-b from-accent/20 to-background">
        <div className="container mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12">Отзывы практикующих</h2>
          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {testimonials.map((testimonial, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow">
                <CardContent className="pt-6">
                  <div className="flex mb-4">
                    {[...Array(5)].map((_, i) => (
                      <Icon key={i} name="Star" className="text-yellow-400 fill-yellow-400" size={18} />
                    ))}
                  </div>
                  <p className="text-muted-foreground mb-4 italic">"{testimonial.text}"</p>
                  <p className="font-medium">— {testimonial.name}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      <section id="faq" className="py-20 px-4">
        <div className="container mx-auto max-w-3xl">
          <h2 className="text-4xl font-bold text-center mb-12">Вопросы и ответы</h2>
          <Accordion type="single" collapsible className="space-y-4">
            {faqs.map((faq, index) => (
              <AccordionItem key={index} value={`item-${index}`} className="border rounded-lg px-6">
                <AccordionTrigger className="text-left hover:no-underline">
                  <span className="font-medium text-lg">{faq.question}</span>
                </AccordionTrigger>
                <AccordionContent className="text-muted-foreground text-base">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </section>

      <section id="contact" className="py-20 px-4 bg-gradient-to-b from-primary/10 to-background">
        <div className="container mx-auto text-center max-w-2xl">
          <h2 className="text-4xl font-bold mb-6">Готовы начать путь?</h2>
          <p className="text-lg text-muted-foreground mb-8">
            Присоединяйтесь к тысячам людей, которые уже меняют свою жизнь с KarmaFlow
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
            <Button size="lg" className="text-lg px-8">
              <Icon name="Mail" className="mr-2" size={20} />
              Написать нам
            </Button>
            <Button size="lg" variant="outline" className="text-lg px-8">
              <Icon name="MessageCircle" className="mr-2" size={20} />
              Telegram
            </Button>
          </div>
          <div className="flex justify-center gap-6 text-muted-foreground">
            <a href="#" className="hover:text-primary transition-colors">
              <Icon name="Instagram" size={24} />
            </a>
            <a href="#" className="hover:text-primary transition-colors">
              <Icon name="Youtube" size={24} />
            </a>
            <a href="#" className="hover:text-primary transition-colors">
              <Icon name="Facebook" size={24} />
            </a>
          </div>
        </div>
      </section>

      <footer className="py-8 px-4 border-t">
        <div className="container mx-auto text-center text-muted-foreground">
          <p>&copy; 2024 KarmaFlow. Все права защищены.</p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
